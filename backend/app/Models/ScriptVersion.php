<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class ScriptVersion extends Model
{
    protected $fillable = [
        'script_id',
        'version_number',
        'file_path',
        'file_size_bytes',
        'change_notes',
        'created_by'
    ];

    public function script()
    {
        return $this->belongsTo(Script::class);
    }
}