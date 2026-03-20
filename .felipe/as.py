

    # Obtener valores de las trackbars
    threshold1 = cv2.getTrackbarPos('Canny Th1', 'Ajustes')
    threshold2 = cv2.getTrackbarPos('Canny Th2', 'Ajustes')
    dilatacion = cv2.getTrackbarPos('Dilatacion', 'Ajustes')
    frecuencia_qr = 10
    # Analizar el frame con los umbrales ajustados
    if iteracion % frecuencia_qr == 0:
        detected_shapes, frame_with_shapes = detect_shapes_in_image(frame, rows, cols, qr_detector)
    else:
        detected_shapes = []  # No analizar formas en esta iteración
        frame_with_shapes = frame  # Reutilizar el frame original# detected_shapes=[{"shape": "triangle","row":1,"col": 0,"cell_index": 3,"x": 100,"y": 100}]
    # moverRobot(tablaQ,cell_index,x,y)
    print("forma",detected_shapes)
    # Dibujar la cuadrícula en el frame

    # Mostrar el frame con los ajustes

    print(f"Estado antes del recorrido: {estado_inicial}")
    estado_inicial = recorrer_mapa(maze, detected_shapes, tablaQ, estado_inicial)
    print(f"El estado recorrió a: {estado_inicial}")
    # Presiona 'q' para salir
    """