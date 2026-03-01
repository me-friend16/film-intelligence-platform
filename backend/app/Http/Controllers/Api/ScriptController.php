<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Script;
use App\Models\ScriptVersion;
use App\Jobs\AnalyzeScript;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class ScriptController extends Controller
{
    protected int $maxFileSize = 52428800; // 50MB

    public function index(Request $request)
    {
        return response()->json([
            'scripts' => $request->user()
                ->scripts()
                ->with('currentVersion')
                ->latest()
                ->paginate(10)
        ]);
    }

    public function upload(Request $request)
    {
        $request->validate([
            'title' => ['required','string','max:255'],
            'file'  => ['required','file','max:' . ($this->maxFileSize / 1024)]
        ]);

        $user = $request->user();

        if (!$user->hasFeature('script-upload')) {
            return response()->json([
                'message' => 'Upload not allowed on your plan.'
            ], 403);
        }

        $file = $request->file('file');
        $filename = Str::uuid() . '.' . $file->getClientOriginalExtension();
        $path = $file->storeAs('scripts/'.$user->id, $filename);

        $script = Script::create([
            'user_id' => $user->id,
            'title' => $request->title,
            'status' => 'analyzing',
            'analysis_status' => 'pending',
        ]);

        $version = ScriptVersion::create([
            'script_id' => $script->id,
            'version_number' => 1,
            'file_path' => $path,
            'file_size_bytes' => $file->getSize(),
            'created_by' => $user->id,
            'change_notes' => 'Initial upload'
        ]);

        $script->update([
            'current_version_id' => $version->id
        ]);

        AnalyzeScript::dispatch($script->id, $version->id);

        return response()->json([
            'message' => 'Script uploaded. Analysis started.',
            'script' => $script->load('currentVersion')
        ], 201);
    }

    public function show(Script $script)
    {
        if ($script->user_id !== auth()->id()) {
            return response()->json(['message' => 'Forbidden'], 403);
        }

        return response()->json([
            'script' => $script->load(['currentVersion','analysisReports'])
        ]);
    }

    public function status(Script $script)
    {
        if ($script->user_id !== auth()->id()) {
            return response()->json(['message' => 'Forbidden'], 403);
        }

        return response()->json([
            'status' => $script->analysis_status,
            'script_status' => $script->status
        ]);
    }

    public function destroy(Script $script)
    {
        if ($script->user_id !== auth()->id()) {
            return response()->json(['message' => 'Forbidden'], 403);
        }

        foreach ($script->versions as $version) {
            Storage::delete($version->file_path);
        }

        $script->delete();

        return response()->json([
            'message' => 'Deleted successfully'
        ]);
    }
}