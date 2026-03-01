<?php

namespace App\Jobs;

use App\Models\Script;
use App\Models\ScriptVersion;
use App\Models\AnalysisReport;
use App\Services\AIEngineService;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Support\Facades\Storage;

class AnalyzeScript implements ShouldQueue
{
    use Queueable;

    public function __construct(
        protected int $scriptId,
        protected int $versionId
    ) {}

    public function handle(AIEngineService $aiService): void
    {
        $script = Script::find($this->scriptId);
        $version = ScriptVersion::find($this->versionId);
        $startedAt = now();

        if (!$script || !$version) {
            return;
        }

        $script->update([
            'analysis_status' => 'processing'
        ]);

        $content = Storage::get($version->file_path);

        $result = $aiService->analyzeScript($content, $script->id);

        if (isset($result['error'])) {
            $script->update([
                'analysis_status' => 'failed',
                'status' => 'draft'
            ]);

            AnalysisReport::create([
                'script_id' => $script->id,
                'script_version_id' => $version->id,
                'status' => 'failed',
                'error_message' => $result['error'],
                'started_at' => $startedAt,
                'completed_at' => now(),
            ]);

            return;
        }

        AnalysisReport::create([
            'script_id' => $script->id,
            'script_version_id' => $version->id,
            'status' => 'completed',
            'structural_metrics' => $result['structural_metrics'] ?? [],
            'continuity_issues' => $result['continuity_issues'] ?? [],
            'character_analysis' => $result['characters'] ?? [],
            'scene_analysis' => $result['scenes'] ?? [],
            
            'sentiment_arc' => $result['sentiment_arc'] ?? null,
            'genre_prediction' => $result['genre_prediction'] ?? null,
            'audience_prediction' => $result['audience_prediction'] ?? null,
            'budget_estimate' => $result['budget_estimate'] ?? null,
            'actor_suggestions' => $result['actor_suggestions'] ?? null,
            'production_risk_flags' => $result['production_risk_flags'] ?? null,

            'processing_time_ms' => $result['processing_time_ms'] ?? null,
            'confidence_score' => $result['confidence_score'] ?? null,
            'started_at' => $startedAt,
            'completed_at' => now()
        ]);

        $script->update([
            'analysis_status' => 'completed',
            'status' => 'analyzed'
        ]);
    }
}