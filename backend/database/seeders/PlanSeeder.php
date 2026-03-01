<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Plan;
use App\Models\Feature;

class PlanSeeder extends Seeder
{
    public function run(): void
    {
        $free = Plan::updateOrCreate(
            ['slug' => 'free'],
            [
                'name' => 'Free',
                'price_cents' => 0,
                'currency' => 'USD',
                'is_active' => true,
                'max_scripts_per_month' => 3,
                'max_storage_mb' => 200,
                'monthly_ai_credits' => 30,
            ]
        );

        $basic = Plan::updateOrCreate(
            ['slug' => 'basic'],
            [
                'name' => 'Basic',
                'price_cents' => 999,
                'currency' => 'USD',
                'is_active' => true,
                'max_scripts_per_month' => 20,
                'max_storage_mb' => 2000,
                'monthly_ai_credits' => 300,
            ]
        );

        $pro = Plan::updateOrCreate(
            ['slug' => 'pro'],
            [
                'name' => 'Pro',
                'price_cents' => 2999,
                'currency' => 'USD',
                'is_active' => true,
                'max_scripts_per_month' => 999,
                'max_storage_mb' => 20000,
                'monthly_ai_credits' => 3000,
            ]
        );

        // Features
        $upload   = Feature::where('slug','script-upload')->first();
        $analyze  = Feature::where('slug','script-analyze')->first();
        $market   = Feature::where('slug','marketplace')->first();
        $casting  = Feature::where('slug','casting-ai')->first();
        $budget   = Feature::where('slug','budget-ai')->first();
        $audience = Feature::where('slug','audience-ai')->first();

        // Free: upload + analyze (limited by credits)
        $free->features()->sync([
            $upload->id => ['limit_value' => null],
            $analyze->id => ['limit_value' => 30],
        ]);

        // Basic: adds audience + budget
        $basic->features()->sync([
            $upload->id => ['limit_value' => null],
            $analyze->id => ['limit_value' => 300],
            $audience->id => ['limit_value' => 120],
            $budget->id => ['limit_value' => 80],
        ]);

        // Pro: everything
        $pro->features()->sync([
            $upload->id => ['limit_value' => null],
            $analyze->id => ['limit_value' => 3000],
            $audience->id => ['limit_value' => 1000],
            $budget->id => ['limit_value' => 600],
            $casting->id => ['limit_value' => 600],
            $market->id => ['limit_value' => null],
        ]);
    }
}