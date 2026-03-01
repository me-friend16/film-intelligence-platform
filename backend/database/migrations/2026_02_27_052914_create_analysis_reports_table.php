<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('analysis_reports', function (Blueprint $table) {
            $table->id();

            $table->foreignId('script_id')->constrained()->cascadeOnDelete();
            $table->foreignId('script_version_id')->constrained()->cascadeOnDelete();

            $table->string('status'); // completed, failed

            $table->json('structural_metrics')->nullable();
            $table->json('continuity_issues')->nullable();
            $table->json('character_analysis')->nullable();
            $table->json('scene_analysis')->nullable();

            $table->integer('processing_time_ms')->nullable();
            $table->float('confidence_score')->nullable();

            $table->timestamp('started_at')->nullable();
            $table->timestamp('completed_at')->nullable();

            $table->text('error_message')->nullable();

            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('analysis_reports');
    }
};