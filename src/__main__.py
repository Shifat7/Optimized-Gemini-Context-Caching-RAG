from src.pipeline import run_pipeline

qs = [
    'What is orbital mechanics?',
    'Describe propulsion systems.',
    'What are deep space missions?'
]

result = run_pipeline('inputs/transcript.txt', qs)
for q, a in result.items():
    print(f'Q: {q}\nA: {a}\n')