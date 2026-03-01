<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('subscriptions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->unique()->constrained()->cascadeOnDelete();
            $table->foreignId('plan_id')->constrained()->restrictOnDelete();

            $table->string('status')->default('active'); // active, canceled, past_due
            $table->timestamp('started_at')->nullable();
            $table->timestamp('ends_at')->nullable();

            // Usage tracking (reset monthly by a job later)
            $table->integer('scripts_used_this_month')->default(0);
            $table->integer('storage_used_mb')->default(0);
            $table->integer('ai_credits_used_this_month')->default(0);

            // Stripe placeholders (future)
            $table->string('provider')->nullable();          // stripe
            $table->string('provider_subscription_id')->nullable();

            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('subscriptions');
    }
};