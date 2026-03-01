<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class RequireFeature
{
    public function handle(Request $request, Closure $next, string $featureSlug): Response
    {
        $user = $request->user();

        if (!$user) {
            return response()->json(['message' => 'Unauthenticated'], 401);
        }

        if (!$user->hasActiveSubscription()) {
            return response()->json([
                'message' => 'Active subscription required.',
            ], 403);
        }

        if (!$user->hasFeature($featureSlug)) {
            return response()->json([
                'message' => 'Feature not available on your plan.',
                'required_feature' => $featureSlug,
                'plan' => $user->plan()?->slug,
            ], 403);
        }

        return $next($request);
    }
}