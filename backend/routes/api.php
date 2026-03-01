<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\ScriptController;

Route::prefix('auth')->group(function () {
    Route::post('/register', [AuthController::class, 'register']);
    Route::post('/login', [AuthController::class, 'login']);
});

Route::middleware('auth:sanctum')->group(function () {

    Route::prefix('auth')->group(function () {
        Route::get('/user', [AuthController::class, 'user']);
        Route::post('/logout', [AuthController::class, 'logout']);
    });

    // ✅ Scripts (protected)
    Route::prefix('scripts')->middleware(['sub'])->group(function () {
        Route::get('/', [ScriptController::class, 'index'])->name('scripts.index');

        Route::post('/', [ScriptController::class, 'upload'])
            ->middleware(['feat:script-upload'])
            ->name('scripts.upload');

        Route::get('/{script}', [ScriptController::class, 'show'])->name('scripts.show');
        Route::get('/{script}/status', [ScriptController::class, 'status'])->name('scripts.status');

        Route::delete('/{script}', [ScriptController::class, 'destroy'])
            ->middleware(['feat:script-upload'])
            ->name('scripts.destroy');
    });

});