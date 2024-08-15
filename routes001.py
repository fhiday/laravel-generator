import os

def generate_routes(table_names):
    routes = ["<?php"]
    for table in table_names:
        model_name = table.capitalize()
        controller_name = f"{model_name}Controller"
        
        routes.append(f"use App\\Http\\Controllers\\{controller_name};")
        routes.append(f"# Routes untuk tabel {table}")
        routes.append(f"Route::get('/{table}', [{controller_name}::class, 'index'])->name('{table}.index');")
        routes.append(f"Route::get('/{table}/create', [{controller_name}::class, 'create'])->name('{table}.create');")
        routes.append(f"Route::post('/{table}', [{controller_name}::class, 'store'])->name('{table}.store');")
        routes.append(f"Route::get('/{table}/{{id}}', [{controller_name}::class, 'show'])->name('{table}.show');")
        routes.append(f"Route::get('/{table}/{{id}}/edit', [{controller_name}::class, 'edit'])->name('{table}.edit');")
        routes.append(f"Route::patch('/{table}/{{id}}', [{controller_name}::class, 'update'])->name('{table}.update');")
        routes.append(f"Route::delete('/{table}/{{id}}', [{controller_name}::class, 'destroy'])->name('{table}.destroy');")
        routes.append("")

    # Membuat direktori jika belum ada
    os.makedirs("output/routes", exist_ok=True)

    with open("output/routes/web.php", "w") as file:
        file.write("\n".join(routes))

# Contoh penggunaan
table_names = ["users", "posts", "comments"]
generate_routes(table_names)