import cv2
import mediapipe as mp
import time

# Inicializar captura de vídeo
cap = cv2.VideoCapture(0) # 0 para webcam ou caminho do arquivo

# Inicializar soluções Mediapipe para mãos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(False)
mpDraw = mp.solutions.drawing_utils

pTime = 0  # Para FPS
cTime = 0

while True:
    success, img = cap.read()
    if not success:
        print("Falha ao capturar imagem.")
        break

    # Converter para RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Processar mãos
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                if id == 0:  # Exemplo: Landmark 0 (base do polegar)
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    # Calcular FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Exibir FPS na imagem
    cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    # Exibir o nome da página na imagem
    cv2.putText(
        img,
        "Instagram: @biomechanicsandcode;"'   ' "Code by Edilson Borba",
        (10, int(img.shape[0]) - 20),  # Ajuste para ficar no canto inferior esquerdo
        cv2.FONT_HERSHEY_SIMPLEX,
        1,  # Escala do texto
        (0, 255, 255),  # Cor do texto (amarelo)
        2,  # Espessura
        cv2.LINE_AA
    )

    # Mostrar a imagem
    cv2.imshow("Image", img)

    # Encerrar ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar os recursos
cap.release()
cv2.destroyAllWindows()
