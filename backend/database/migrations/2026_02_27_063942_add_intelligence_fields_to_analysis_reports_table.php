<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('analysis_reports', function (Blueprint $table) {
            $table->json('audience_prediction')->nullable();
            $table->json('genre_prediction')->nullable();
            $table->json('budget_estimate')->nullable();
            $table->json('actor_suggestions')->nullable();
            $table->json('production_risk_flags')->nullable();
        });
    }

    public function down(): void
    {
        Schema::table('analysis_reports', function (Blueprint $table) {
            $table->dropColumn([
                'audience_prediction',
                'genre_prediction',
                'budget_estimate',
                'actor_suggestions',
                'production_risk_flags'
            ]);
        });
    }
};