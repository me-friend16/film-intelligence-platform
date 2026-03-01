<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('plans', function (Blueprint $table) {
            $table->id();
            $table->string('name');               // Free, Basic, Pro
            $table->string('slug')->unique();     // free, basic, pro
            $table->integer('price_cents')->default(0);
            $table->string('currency', 10)->default('USD');
            $table->boolean('is_active')->default(true);

            // Limits
            $table->integer('max_scripts_per_month')->default(0);
            $table->integer('max_storage_mb')->default(0);
            $table->integer('monthly_ai_credits')->default(0); // for future metered AI

            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('plans');
    }
};