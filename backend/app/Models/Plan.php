<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Plan extends Model
{
    protected $fillable = [
        'name','slug','price_cents','currency','is_active',
        'max_scripts_per_month','max_storage_mb','monthly_ai_credits'
    ];

    public function features()
    {
        return $this->belongsToMany(Feature::class, 'plan_feature')
            ->withPivot(['limit_value']);
    }

    public function subscriptions()
    {
        return $this->hasMany(Subscription::class);
    }

    public function hasFeature(string $slug): bool
    {
        return $this->features()->where('slug', $slug)->exists();
    }
}