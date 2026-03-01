<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Permission;
use App\Models\Role;

class PermissionSeeder extends Seeder
{
    public function run(): void
    {
        $permissions = [
            // Core platform
            ['name' => 'Access Admin Panel', 'slug' => 'access-admin', 'description' => 'Can access admin APIs'],
            ['name' => 'Manage Users',       'slug' => 'manage-users', 'description' => 'Can manage users'],
            ['name' => 'Manage Plans',       'slug' => 'manage-plans', 'description' => 'Can manage subscription plans'],
            ['name' => 'Manage Finance',     'slug' => 'manage-finance', 'description' => 'Can manage finance & payouts'],
            ['name' => 'Manage Content',     'slug' => 'manage-content', 'description' => 'Can moderate content'],
            ['name' => 'Manage System',      'slug' => 'manage-system', 'description' => 'Can manage system settings'],

            // Script platform
            ['name' => 'Upload Script',      'slug' => 'script-upload', 'description' => 'Can upload scripts'],
            ['name' => 'Analyze Script',     'slug' => 'script-analyze', 'description' => 'Can request analysis'],
            ['name' => 'Publish Script',     'slug' => 'script-publish', 'description' => 'Can publish to marketplace'],
        ];

        foreach ($permissions as $perm) {
            Permission::updateOrCreate(['slug' => $perm['slug']], $perm);
        }

        // Attach permissions to roles
        $superadmin = Role::where('slug', 'superadmin')->first();
        $admin      = Role::where('slug', 'admin')->first();
        $moderator  = Role::where('slug', 'moderator')->first();
        $support    = Role::where('slug', 'support')->first();
        $writer     = Role::where('slug', 'writer')->first();
        $producer   = Role::where('slug', 'producer')->first();
        $director   = Role::where('slug', 'director')->first();
        $actor      = Role::where('slug', 'actor')->first();

        $allPermIds = Permission::pluck('id')->all();

        if ($superadmin) $superadmin->permissions()->sync($allPermIds);

        if ($admin) {
            $admin->permissions()->sync(Permission::whereIn('slug', [
                'access-admin','manage-users','manage-plans','manage-finance','manage-content'
            ])->pluck('id')->all());
        }

        if ($moderator) {
            $moderator->permissions()->sync(Permission::whereIn('slug', [
                'access-admin','manage-content'
            ])->pluck('id')->all());
        }

        if ($support) {
            $support->permissions()->sync(Permission::whereIn('slug', [
                'access-admin','manage-users'
            ])->pluck('id')->all());
        }

        $creatorPerms = Permission::whereIn('slug', ['script-upload','script-analyze','script-publish'])->pluck('id')->all();
        foreach ([$writer, $producer, $director, $actor] as $r) {
            if ($r) $r->permissions()->sync($creatorPerms);
        }
    }
}