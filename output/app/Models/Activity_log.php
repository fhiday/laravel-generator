<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Activity_log extends Model
{
    use HasFactory;

    protected $table = 'activity_log';
    protected $fillable = ['log_name', 'description', 'subject_type', 'event', 'subject_id', 'causer_type', 'causer_id', 'properties', 'batch_uuid'];
    protected $primaryKey = 'id';

    // Tidak ada foreign key yang ditemukan
}
