<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Script extends Model
{
    protected $fillable = [
        'user_id',
        'title',
        'logline',
        'synopsis',
        'status',
        'analysis_status',
        'current_version_id',
        'page_count'
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function versions()
    {
        return $this->hasMany(ScriptVersion::class);
    }

    public function currentVersion()
    {
        return $this->belongsTo(ScriptVersion::class, 'current_version_id');
    }

    public function analysisReports()
    {
        return $this->hasMany(AnalysisReport::class);
    }
}