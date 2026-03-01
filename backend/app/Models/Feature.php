<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Feature extends Model
{
    protected $fillable = [
        'name', 'slug', 'description', 'is_metered'
    ];

    public function plans()
    {
        return $this->belongsToMany(Plan::class, 'plan_feature')
            ->withPivot(['limit_value']);
    }
}