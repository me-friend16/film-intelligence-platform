<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Feature;

class FeatureSeeder extends Seeder
{
    public function run(): void
    {
        $features = [
            ['name' => 'Script Upload',  'slug' => 'script-upload',  'description' => 'Upload scripts', 'is_metered' => false],
            ['name' => 'Script Analyze', 'slug' => 'script-analyze', 'description' => 'Analyze scripts', 'is_metered' => true],
            ['name' => 'Marketplace',    'slug' => 'marketplace',   'description' => 'Access marketplace', 'is_metered' => false],
            ['name' => 'Casting AI',     'slug' => 'casting-ai',    'description' => 'Casting suggestions', 'is_metered' => true],
            ['name' => 'Budget AI',      'slug' => 'budget-ai',     'description' => 'Budget estimation', 'is_metered' => true],
            ['name' => 'Audience AI',    'slug' => 'audience-ai',   'description' => 'Audience prediction', 'is_metered' => true],
        ];

        foreach ($features as $f) {
            Feature::updateOrCreate(['slug' => $f['slug']], $f);
        }
    }
}