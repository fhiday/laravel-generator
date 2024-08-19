import os

def generate_routes(table_names, dbname):
    routes = ["<?php"]
    for table in table_names:
        model_name = table.capitalize()
        controller_name = f"{model_name}Controller"
        
        #routes.append(f"use App\\Http\\Controllers\\{controller_name};")
        routes.append(f"# Routes untuk tabel {table}")
        routes.append(f"Route::resource('{table}', App\\Http\\Controllers\\{controller_name}::class);")
        routes.append("")

    # Membuat direktori jika belum ada
    os.makedirs("output/"+dbname+"/routes", exist_ok=True)

    with open("output/"+dbname+"/routes/web.php", "w") as file:
        file.write("\n".join(routes))

# Contoh penggunaan
#table_names = ["users", "posts", "comments"]
#generate_routes(table_names)