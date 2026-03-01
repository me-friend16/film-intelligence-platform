<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Role;

class RoleSeeder extends Seeder
{
    public function run(): void
    {
        $roles = [
            ['name' => 'Super Admin', 'slug' => 'superadmin', 'description' => 'Full system access', 'is_system' => true],
            ['name' => 'Admin',       'slug' => 'admin',      'description' => 'Admin access',       'is_system' => true],
            ['name' => 'Moderator',   'slug' => 'moderator',  'description' => 'Moderation access',  'is_system' => true],
            ['name' => 'Support',     'slug' => 'support',    'description' => 'Support access',     'is_system' => true],

            ['name' => 'Writer',      'slug' => 'writer',     'description' => 'Script writer',      'is_system' => false],
            ['name' => 'Producer',    'slug' => 'producer',   'description' => 'Producer',           'is_system' => false],
            ['name' => 'Director',    'slug' => 'director',   'description' => 'Director',           'is_system' => false],
            ['name' => 'Actor',       'slug' => 'actor',      'description' => 'Actor',              'is_system' => false],
        ];

        foreach ($roles as $role) {
            Role::updateOrCreate(['slug' => $role['slug']], $role);
        }
    }
}