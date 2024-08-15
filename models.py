def generate_model(table):
    model_name = table.name.capitalize()
    columns = table.columns.keys()
    primary_key = next((col.name for col in table.columns if col.primary_key), 'id')
    
    # Hanya menyertakan kolom yang diperlukan dalam fillable
    fillable_columns = [col for col in columns if col not in ['id', 'created_at', 'updated_at']]

    # Mencari foreign key dan membuat relasi
    relations = []
    has_foreign_key = False
    for col in table.columns:
        if col.foreign_keys:
            has_foreign_key = True
            related_column = next(iter(col.foreign_keys)).column.name
            related_table = next(iter(col.foreign_keys)).column.table.name
            related_model = related_table.capitalize()
            relations.append(f"public function {related_table}() {{ return $this->belongsTo({related_model}::class,'{col.name}'); }}")

    if not has_foreign_key:
        relations.append("// Tidak ada foreign key yang ditemukan")

    model_template = f"""<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Database\\Eloquent\\Model;
use Spatie\\Activitylog\\LogOptions;
use Spatie\\Activitylog\\Traits\\LogsActivity;

class {model_name} extends Model
{{
    use HasFactory, LogsActivity;

    protected $table = '{table.name}';
    protected $fillable = [{', '.join([f"'{col}'" for col in fillable_columns])}];
    protected $primaryKey = '{primary_key}';

    public function getActivitylogOptions(): LogOptions
    {{
        return LogOptions::defaults()
            ->logOnly([{', '.join([f"'{col}'" for col in fillable_columns])}])
            ->setDescriptionForEvent(fn(string $eventName) => "This model has been {{$eventName}}")
            ->useLogName('{model_name}');
    }}

    {' '.join(relations)}
}}
"""
    with open(f"output/app/Models/{model_name}.php", "w") as file:
        file.write(model_template)
