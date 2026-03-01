<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class AIEngineService
{
    protected string $baseUrl;
    protected int $timeout;

    public function __construct()
    {
        $this->baseUrl = config('services.ai_engine.url', 'http://ai-engine:8000');
        $this->timeout = (int) config('services.ai_engine.timeout', 300);
    }

    /**
     * Analyze script via AI Engine (JSON payload)
     */
    public function analyzeScript(string $fileContent, int $scriptId): array
    {
        try {
            $response = Http::timeout($this->timeout)
                ->acceptJson()
                ->asJson()
                ->post("{$this->baseUrl}/analyze", [
                    'script_id' => $scriptId,
                    'text' => $fileContent,
                ]);

            if ($response->successful()) {
                return $response->json();
            }

            Log::error('AI Engine analysis failed', [
                'script_id' => $scriptId,
                'status' => $response->status(),
                'response' => $response->body(),
            ]);

            return ['error' => 'Analysis failed: ' . $response->body()];
        } catch (\Exception $e) {
            Log::error('AI Engine request failed', [
                'script_id' => $scriptId,
                'error' => $e->getMessage(),
            ]);

            return ['error' => 'Request failed: ' . $e->getMessage()];
        }
    }

    /**
     * Health check
     */
    public function healthCheck(): array
    {
        try {
            $response = Http::timeout(10)->get("{$this->baseUrl}/health");

            if ($response->successful()) {
                return ['status' => 'healthy', 'data' => $response->json()];
            }

            return ['status' => 'unhealthy', 'error' => 'Status: ' . $response->status()];
        } catch (\Exception $e) {
            return ['status' => 'unhealthy', 'error' => $e->getMessage()];
        }
    }
}