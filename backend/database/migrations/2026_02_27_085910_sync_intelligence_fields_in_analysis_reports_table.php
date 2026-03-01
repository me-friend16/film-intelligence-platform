<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('analysis_reports', function (Blueprint $table) {
            if (!Schema::hasColumn('analysis_reports', 'sentiment_arc')) {
                $table->json('sentiment_arc')->nullable()->after('scene_analysis');
            }
            if (!Schema::hasColumn('analysis_reports', 'genre_prediction')) {
                $table->json('genre_prediction')->nullable()->after('sentiment_arc');
            }
            if (!Schema::hasColumn('analysis_reports', 'audience_prediction')) {
                $table->json('audience_prediction')->nullable()->after('genre_prediction');
            }
            if (!Schema::hasColumn('analysis_reports', 'budget_estimate')) {
                $table->json('budget_estimate')->nullable()->after('audience_prediction');
            }
            if (!Schema::hasColumn('analysis_reports', 'actor_suggestions')) {
                $table->json('actor_suggestions')->nullable()->after('budget_estimate');
            }
            if (!Schema::hasColumn('analysis_reports', 'production_risk_flags')) {
                $table->json('production_risk_flags')->nullable()->after('actor_suggestions');
            }
        });
    }

    public function down(): void
    {
        // Keep down empty for safety (sync migrations are not meant to rollback)
    }
};