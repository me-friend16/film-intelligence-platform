<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Subscription extends Model
{
    protected $fillable = [
        'user_id','plan_id','status','started_at','ends_at',
        'scripts_used_this_month','storage_used_mb','ai_credits_used_this_month',
        'provider','provider_subscription_id'
    ];

    protected $casts = [
        'started_at' => 'datetime',
        'ends_at' => 'datetime',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function plan()
    {
        return $this->belongsTo(Plan::class);
    }

    public function isActive(): bool
    {
        if ($this->status !== 'active') return false;
        if ($this->ends_at && now()->greaterThan($this->ends_at)) return false;
        return true;
    }
}