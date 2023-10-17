front_back_prompt = [{"role": "system", "content":
'''
Task: Your task is to convert the text from the user into Basic Note Type (front/back) Anki flashcards. Prioritize information regarding principles in computer science and those needed for majoring in computer science. Ensure that each flashcard is clearly written, and adheres to the specified formatting and reference criteria.

Formatting Criteria:

- Construct an list (python) that contains lists where each inner list represent one flashcard.
- The first element of a inner list should contain a statement testing the computer science understanding of a student.
- The second element of the inner list should contain the succinct answer to the question.
- The List always looks like this: [['Question1','Answer1'],['Question2','Answer2']] with the possibility to have more then 1 Flashcard.

Reference Criteria for each \"Statement\":

- Each flashcard should test a single concept
- Limit the word count of each question to less than 40 words.
- Each flashcard MUST be able to stand alone. Include the subject of the flashcard somewhere in the text.
- Keep ONLY simple, direct questions in the first element of an inner list column.

'''},

{"role": "system", "name": "example_user", "content": '''In computer science, a thread of execution is the smallest sequence of programmed instructions that can be managed independently by a scheduler, which is typically a part of the operating system. In many cases, a thread is a component of a process.

The multiple threads of a given process may be executed concurrently (via multithreading capabilities), sharing resources such as memory, while different processes do not share these resources. In particular, the threads of a process share its executable code and the values of its dynamically allocated variables and non-thread-local global variables at any given time.'''},
{"role": "system", "name": "example_assistent", "content": '''[['What is a thread of execution in computer science?',
 ' In computer science, a thread of execution is the smallest sequence of programmed instructions that can be managed independently by a scheduler, which is typically a part of the operating system. In many cases, a thread is a component of a process.'],['What is the key distinction between threads and processes in computer science, especially concerning resource sharing?','Threads and processes in computer science differ primarily in their resource-sharing capabilities. Threads are the smallest units of execution, managed by an OS scheduler, and multiple threads within a process can run concurrently. They share resources like memory, executable code, and variable values. In contrast, different processes do not share these resources, making threads a more efficient way to achieve concurrency while ensuring resource isolation between processes.']]'''}]