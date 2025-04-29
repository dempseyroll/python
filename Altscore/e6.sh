#!/usr/bin/env bash

# Lista fija de tipos a considerar (ordenada alfabéticamente)
TYPES=('bug' 'dark' 'dragon' 'electric' 'fairy' 'fighting' 'fire' 'flying' 'ghost' 'grass' 'ground' 'ice' 'normal' 'poison' 'psychic' 'rock' 'steel' 'water')

# Archivos temporales para contadores
COUNT_FILE=$(mktemp)
HEIGHT_FILE=$(mktemp)

# Inicializar archivos con ceros
for _ in "${TYPES[@]}"; do
    echo 0 >> "$COUNT_FILE"
    echo 0 >> "$HEIGHT_FILE"
done

# Recorre todos los Pokémon desde la API paginada
url="https://pokeapi.co/api/v2/pokemon"

while [ -n "$url" ]; do
    echo "Procesando página: $url"
    response=$(curl -s "$url")
    url=$(echo "$response" | jq -r '.next')

    echo "$response" | jq -c '.results[]' | while read -r pokemon; do
        poke_url=$(echo "$pokemon" | jq -r '.url')
        poke_data=$(curl -s "$poke_url")

        height=$(echo "$poke_data" | jq -r '.height')
        types=$(echo "$poke_data" | jq -r '.types[].type.name')

        for type in $types; do
            echo "Tipo encontrado: $type"  # Depuración para ver los tipos encontrados

            for i in "${!TYPES[@]}"; do
                if [[ "$type" == "${TYPES[$i]}" ]]; then
                    # Leer el contador y el total de altura de los archivos
                    count=$(sed -n "$((i+1))p" "$COUNT_FILE")
                    total=$(sed -n "$((i+1))p" "$HEIGHT_FILE")

                    # Incrementar contador y sumar altura
                    count=$((count + 1))
                    total=$((total + height))

                    # Reescribir los archivos con los nuevos valores
                    sed -n "$((i+1))p" "$COUNT_FILE" > temp_count.txt
                    sed -n "$((i+1))p" "$HEIGHT_FILE" > temp_height.txt

                    # Sobrescribir el archivo original
                    sed -i '' "$((i+1))s/.*/$count/" "$COUNT_FILE"
                    sed -i '' "$((i+1))s/.*/$total/" "$HEIGHT_FILE"

                    # Depuración de lo que se está sumando
                    echo "Actualizado tipo $type: contador=$count, altura total=$total"
                fi
            done
        done
    done
done

# Construir JSON ordenado alfabéticamente
echo "{"
for i in "${!TYPES[@]}"; do
    type="${TYPES[$i]}"
    count=$(sed -n "$((i+1))p" "$COUNT_FILE")
    total=$(sed -n "$((i+1))p" "$HEIGHT_FILE")

    if [ "$count" -ne 0 ]; then
        avg=$(echo "scale=3; $total / $count" | bc)
    else
        avg="null"
    fi

    # Coma si no es el último
    if [ "$i" -lt "$((${#TYPES[@]} - 1))" ]; then
        echo "  \"$type\": $avg,"
    else
        echo "  \"$type\": $avg"
    fi
done
echo "}"

# Limpiar archivos temporales
rm "$COUNT_FILE" "$HEIGHT_FILE"
