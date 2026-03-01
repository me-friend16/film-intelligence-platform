<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class AnalysisReport extends Model
{
    use HasFactory;

    protected $fillable = [
        'script_id',
        'script_version_id',
        'status',
        'structural_metrics',
        'continuity_issues',
        'character_analysis',
        'scene_analysis',
        'sentiment_arc',
        'genre_prediction',
        'audience_prediction',
        'budget_estimate',
        'actor_suggestions',
        'production_risk_flags',
        'processing_time_ms',
        'confidence_score',
        'started_at',
        'completed_at',
        'error_message',
    ];

    protected $casts = [
        'structural_metrics' => 'array',
        'continuity_issues' => 'array',
        'character_analysis' => 'array',
        'scene_analysis' => 'array',
        'sentiment_arc' => 'array',
        'genre_prediction' => 'array',
        'audience_prediction' => 'array',
        'budget_estimate' => 'array',
        'actor_suggestions' => 'array',
        'production_risk_flags' => 'array',
        'started_at' => 'datetime',
        'completed_at' => 'datetime',
    ];

    public function script()
    {
        return $this->belongsTo(Script::class);
    }

    public function version()
    {
        return $this->belongsTo(ScriptVersion::class, 'script_version_id');
    }
}