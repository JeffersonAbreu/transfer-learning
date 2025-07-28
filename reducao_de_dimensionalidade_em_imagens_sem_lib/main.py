import os
from PIL import Image

def converter_imagem_para_cinza_e_gerar_arquivo(caminho_da_imagem_original, nome_da_imagem_cinza_saida="output_gray.png"):
    caminho_completo_original = full_path(caminho_da_imagem_original)

    if caminho_completo_original is None:
        return False # Retorna False em caso de erro

    print(f"Iniciando o processamento para tons de cinza da imagem: {caminho_completo_original}")

    try:
        imagem_colorida = Image.open(caminho_completo_original)#.convert('RGB') # Garante que a imagem esteja em RGB
        largura, altura = imagem_colorida.size

        print(f"Imagem '{caminho_completo_original}' carregada com sucesso. Dimensões: {largura}x{altura} pixels.")

        pixels_em_cinza = []

        for y in range(altura):
            linha_de_pixels_em_cinza = []
            for x in range(largura):
                r, g, b = imagem_colorida.getpixel((x, y))
                valor_cinza = int((r + g + b) / 3) # Conversão manual para cinza
                linha_de_pixels_em_cinza.append(valor_cinza)
            pixels_em_cinza.append(linha_de_pixels_em_cinza)

        imagem_cinza_pillow = Image.new('L', (largura, altura))

        for y in range(altura):
            for x in range(largura):
                imagem_cinza_pillow.putpixel((x, y), pixels_em_cinza[y][x])

        diretorio_do_script = os.path.dirname(os.path.abspath(__file__))
        caminho_completo_saida = os.path.join(diretorio_do_script, nome_da_imagem_cinza_saida)
        
        imagem_cinza_pillow.save(caminho_completo_saida)

        print(f"Imagem em tons de cinza GERADA e SALVA como: '{caminho_completo_saida}'")
        print("Processamento para tons de cinza concluído.")
        return True
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao processar ou salvar a imagem para tons de cinza: {e}")
    return False

def converter_imagem_para_pb_e_gerar_arquivo(caminho_da_imagem_original, nome_da_imagem_de_saida="output_pb.png"):
    caminho_completo_original = full_path(caminho_da_imagem_original)

    if caminho_completo_original is None:
        return False # Retorna False em caso de erro

    print(f"Iniciando o processamento para P&B da imagem: {caminho_completo_original}")
    try:
        imagem_cinza = Image.open(caminho_completo_original)#.convert('L') # Abre como cinza diretamente
        largura, altura = imagem_cinza.size

        print(f"Imagem '{caminho_completo_original}' carregada com sucesso. Dimensões: {largura}x{altura} pixels.")

        pixels_pb = []
        # Defina um limiar para a binarização. 160 é um bom ponto de partida, mas pode ser ajustado.
        limiar_pb = int(256/2)

        # Itera sobre cada pixel da imagem em tons de cinza para binarizar manualmente
        for y in range(altura):
            linha_de_pixels_pb = []
            for x in range(largura):
                val_cinza = imagem_cinza.getpixel((x, y))
                # Se o valor de cinza for maior que o limiar, torna branco (255), senão preto (0)
                val_pb = 255 if val_cinza > limiar_pb else 0
                linha_de_pixels_pb.append(val_pb)
            pixels_pb.append(linha_de_pixels_pb)

        imagem_pb_pillow = Image.new('1', (largura, altura)) # '1' para modo binário (preto e branco puro)

        for y in range(altura):
            for x in range(largura):
                imagem_pb_pillow.putpixel((x, y), pixels_pb[y][x])

        diretorio_do_script = os.path.dirname(os.path.abspath(__file__))
        caminho_completo_saida = os.path.join(diretorio_do_script, nome_da_imagem_de_saida)
        
        imagem_pb_pillow.save(caminho_completo_saida)

        print(f"Imagem P&B GERADA e SALVA como: '{caminho_completo_saida}'")
        print("Processamento para P&B concluído.")
        return True
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao processar ou salvar a imagem para P&B: {e}")
    return False
    
def full_path(name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, name)
    if not os.path.exists(img_path):
        print(f"ERRO: O arquivo '{img_path}' NÃO FOI ENCONTRADO.")
        print("Por favor, verifique se o nome/caminho da imagem está correto e se ela está na mesma pasta do script.")
        return None
    return img_path

if __name__ == "__main__":
    name_img = "lena_original.png" # Sua imagem colorida de entrada
    output_gray_name = "lena_gray.png" # Nome do arquivo de saída em tons de cinza
    output_pb_name = "lena_pb.png"     # Nome do arquivo de saída em preto e branco

    # 1. Converte a imagem original para tons de cinza
    if converter_imagem_para_cinza_e_gerar_arquivo(name_img, output_gray_name):
        # 2. Se a imagem em tons de cinza foi gerada com sucesso, converte-a para P&B
        # Usamos 'output_gray_name' como entrada para a função de P&B, pois ela já está em cinza.
        converter_imagem_para_pb_e_gerar_arquivo(output_gray_name, output_pb_name)