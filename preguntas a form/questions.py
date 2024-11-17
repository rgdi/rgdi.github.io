import pdfplumber
import re
import json

def extract_questions_from_pdf(pdf_path):
    questions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            
            # Dividir el texto en líneas
            lines = text.split('\n')
            question = None
            options = []
            answer_index = None
            
            for line in lines:
                line = line.strip()
                
                # Identificar preguntas (asumiendo que comienzan con un número)
                if re.match(r'^\d+ª/', line):
                    if question and options:
                        # Guardar la pregunta anterior
                        questions.append({
                            'question': question,
                            'options': options,
                            'answer': answer_index
                        })
                        options = []  # Reiniciar opciones
                    
                    # Extraer la pregunta
                    question_match = re.search(r'^\d+ª/ (.+)', line)
                    if question_match:
                        question = question_match.group(1)
                        answer_index = None  # Reiniciar el índice de respuesta

                # Identificar opciones
                elif re.match(r'^[a-e]\)', line):
                    option_text = line[3:].strip()  # Extraer texto de la opción
                    options.append(option_text)

                    # Aquí puedes añadir lógica para identificar la respuesta correcta
                    # Si la opción correcta está marcada de alguna manera (ej. con un asterisco)
                    if '*' in option_text:  # Cambia esto según cómo se marque en el PDF
                        answer_index = len(options) - 1  # Guardar el índice de la opción correcta

            # Guardar la última pregunta después de salir del bucle
            if question and options:
                questions.append({
                    'question': question,
                    'options': options,
                    'answer': answer_index
                })

    return questions

def save_questions_to_txt(questions, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for q in questions:
            file.write(json.dumps(q, ensure_ascii=False) + '\n')

def main():
    pdf_path = 'preguntastema1.pdf'  # Cambia esto por la ruta de tu PDF
    output_path = 'questions.txt'
    
    questions = extract_questions_from_pdf(pdf_path)
    
    if questions:
        save_questions_to_txt(questions, output_path)
        print(f"Las preguntas se han guardado en {output_path}")
    else:
        print("No se encontraron preguntas en el PDF.")

if __name__ == "__main__":
    main()