<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('scripts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();

            $table->string('title');
            $table->text('logline')->nullable();
            $table->text('synopsis')->nullable();

            $table->string('status')->default('draft'); // draft, analyzing, analyzed
            $table->string('analysis_status')->default('pending'); // pending, processing, completed, failed

            $table->unsignedBigInteger('current_version_id')->nullable();

            $table->integer('page_count')->nullable();

            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('scripts');
    }
};