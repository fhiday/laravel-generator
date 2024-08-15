def generate_controller(table):
    model_name = table.name.capitalize()
    controller_name = f"{model_name}Controller"
    
    primary_key = next((col.name for col in table.columns if col.primary_key), 'id')
    
    # Mencari foreign key dan membuat relasi
    relations = []
    has_foreign_key = False
    for col in table.columns:
        if col.foreign_keys:
            has_foreign_key = True
            related_table = next(iter(col.foreign_keys)).column.table.name
            related_model = related_table.capitalize()
            relations.append(f"${related_table} = {related_model}::all();")

    controller_template = f"""<?php

namespace App\\Http\\Controllers;

use App\\Models\\{model_name};
use Illuminate\\Http\\Request;
use Illuminate\\Support\\Facades\\Validator;
{''.join([f'use App\\Models\\{next(iter(col.foreign_keys)).column.table.name.capitalize()};' for col in table.columns if col.foreign_keys])}

class {controller_name} extends Controller
{{
    public function index()
    {{
        $data = {model_name}::all();
        return view('{table.name}.index', compact('data'));
    }}

    public function create()
    {{
        {''.join(relations)}
        return view('{table.name}.create', compact({', '.join([f"'{next(iter(col.foreign_keys)).column.table.name}'" for col in table.columns if col.foreign_keys])}));
    }}

    public function store(Request $request)
    {{
        $validator = Validator::make($request->all(), [
            {', '.join([f"'{col}' => 'required'" for col in table.columns.keys() if col not in [primary_key, 'created_at', 'updated_at']])}
        ]);

        if ($validator->fails()) {{
            return redirect()->route('{table.name}.create')
                             ->withErrors($validator)
                             ->withInput();
        }}

        {model_name}::create($validator->validated());
        return redirect()->route('{table.name}.index');
    }}

    public function show($id)
    {{
        $data = {model_name}::findOrFail($id);
        return view('{table.name}.show', compact('data'));
    }}

    public function edit($id)
    {{
        $data = {model_name}::findOrFail($id);
        {''.join(relations)}
        return view('{table.name}.edit', compact('data', {', '.join([f"'{next(iter(col.foreign_keys)).column.table.name}'" for col in table.columns if col.foreign_keys])}));
    }}

    public function update(Request $request, $id)
    {{
        $validator = Validator::make($request->all(), [
            {', '.join([f"'{col}' => 'required'" for col in table.columns.keys() if col not in [primary_key, 'created_at', 'updated_at']])}
        ]);

        if ($validator->fails()) {{
            return redirect()->route('{table.name}.edit', ['id' => $id])
                             ->withErrors($validator)
                             ->withInput();
        }}

        $data = {model_name}::findOrFail($id);
        $data->update($validator->validated());
        return redirect()->route('{table.name}.index');
    }}

    public function destroy($id)
    {{
        $data = {model_name}::findOrFail($id);
        $data->delete();
        return redirect()->route('{table.name}.index');
    }}
}}
"""
    with open(f"output/app/Http/Controllers/{controller_name}.php", "w") as file:
        file.write(controller_template)
