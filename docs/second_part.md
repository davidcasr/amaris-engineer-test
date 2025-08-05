# 📄 Parte 2 - Consulta SQL

## 🧾 Enunciado

Obtener los nombres de los clientes los cuales tienen inscrito algún producto disponible sólo en las sucursales que visitan.

## 🧠 Explicación

Esta consulta busca seleccionar a los clientes que están inscritos a un producto, y además dicho producto **solo se encuentra disponible en las sucursales que ese cliente ha visitado**. Es decir, si el producto está disponible en una sucursal que el cliente **no ha visitado**, se excluye.

## ✅ Consulta SQL

```sql
SELECT DISTINCT c.nombre
FROM Cliente c
JOIN Inscripción i ON c.id = i.idCliente
JOIN Disponibilidad d ON i.idProducto = d.idProducto
WHERE NOT EXISTS (
  SELECT 1
  FROM Disponibilidad d2
  WHERE d2.idProducto = i.idProducto
    AND d2.idSucursal NOT IN (
      SELECT v.idSucursal
      FROM Visitan v
      WHERE v.idCliente = c.id
    )
)
```
