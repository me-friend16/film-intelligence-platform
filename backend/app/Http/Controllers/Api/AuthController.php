<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Role;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\Rules\Password;
use Illuminate\Validation\ValidationException;
use App\Models\Subscription;
use App\Models\Plan;

class AuthController extends Controller
{
    /**
     * Register new user (API token auth via Sanctum)
     */
    public function register(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name'        => ['required', 'string', 'max:255'],
            'email'       => ['required', 'string', 'email', 'max:255', 'unique:users,email'],
            'password'    => ['required', 'confirmed', Password::defaults()],
            'role'        => ['required', 'string', 'in:writer,producer,director,actor'],
            'device_name' => ['required', 'string', 'max:255'],
        ]);

        $role = Role::where('slug', $validated['role'])->firstOrFail();

        $user = User::create([
            'name'     => $validated['name'],
            'email'    => $validated['email'],
            'password' => Hash::make($validated['password']),
            'role_id'  => $role->id,
            'is_active'=> true,
        ]);

        $token = $user->createToken($validated['device_name'], ['*']);

        $freePlan = Plan::where('slug', 'free')->first();

        Subscription::updateOrCreate(
            ['user_id' => $user->id],
            [
                'plan_id' => $freePlan->id,
                'status' => 'active',
                'started_at' => now(),
                'scripts_used_this_month' => 0,
                'storage_used_mb' => 0,
                'ai_credits_used_this_month' => 0,
            ]
        );

        return response()->json([
            'message' => 'Registration successful',
            'user' => $user->load('role'),
            'token' => $token->plainTextToken,
            'token_type' => 'Bearer',
        ], 201);
    }

    /**
     * Login user
     */
    public function login(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'email'       => ['required', 'string', 'email'],
            'password'    => ['required', 'string'],
            'device_name' => ['required', 'string', 'max:255'],
        ]);

        $user = User::where('email', $validated['email'])->first();

        if (!$user || !Hash::check($validated['password'], $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['The provided credentials are incorrect.'],
            ]);
        }

        if (!$user->is_active) {
            return response()->json([
                'message' => 'Account is disabled.',
            ], 403);
        }

        // Optional: revoke tokens for same device name to prevent accumulation
        $user->tokens()->where('name', $validated['device_name'])->delete();

        $user->update([
            'last_login_at' => now(),
            'last_login_ip' => $request->ip(),
        ]);

        $token = $user->createToken($validated['device_name'], ['*']);

        return response()->json([
            'message' => 'Login successful',
            'user' => $user->load('role'),
            'token' => $token->plainTextToken,
            'token_type' => 'Bearer',
        ]);
    }

    /**
     * Current authenticated user
     */
    public function user(Request $request): JsonResponse
    {
        return response()->json([
            'user' => $request->user()->load('role'),
        ]);
    }

    /**
     * Logout current token
     */
    public function logout(Request $request): JsonResponse
    {
        $request->user()->currentAccessToken()?->delete();

        return response()->json([
            'message' => 'Logged out successfully',
        ]);
    }
}