<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('script_versions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('script_id')->constrained()->cascadeOnDelete();

            $table->integer('version_number');
            $table->string('file_path');
            $table->unsignedBigInteger('file_size_bytes');

            $table->text('change_notes')->nullable();
            $table->foreignId('created_by')->constrained('users')->cascadeOnDelete();

            $table->timestamps();

            $table->unique(['script_id', 'version_number']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('script_versions');
    }
};