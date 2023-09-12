import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { PaperCurriculum, Question, getAllAnswers } from '@models';

@Injectable({
  providedIn: 'root'
})
export class ContentService {
  private paperCurriculum: PaperCurriculum = {
    overview_module: {
      name: 'Attention is All You Need',
      blurb: `Introduction:

Traditional models for sequence-to-sequence tasks, like translating English to French, relied on recurrent neural networks (RNNs) or long short-term memory (LSTM) networks. These models process data in order, which can be slow and may not capture long-range dependencies well.
The Transformer architecture was introduced as a solution to these problems, focusing on a mechanism called "attention" to draw global dependencies between input and output.

Attention Mechanism:


The core idea behind attention is to weigh the importance of different parts of the input when producing an output. For instance, when translating the word "it" in a sentence, the model might need to look back at a noun mentioned earlier to understand what "it" refers to.
The Transformer uses a specific type of attention called "scaled dot-product attention." This mechanism computes a weighted sum of values based on their relevance to a given query.

Multi-Head Attention:

Instead of having one set of attention weights, the Transformer uses multiple sets, allowing it to focus on different parts of the input simultaneously. This is called "multi-head attention."
This allows the model to capture various aspects of the information, like both the meaning and the grammatical role of a word in a sentence.

Positional Encoding:

Since the Transformer doesn't process data in order like RNNs, it needs a way to consider the position of words in a sequence.
"Positional encodings" are added to the embeddings at the input layer to provide this positional information. These encodings ensure that the model can consider word order.

Feed-forward Neural Networks:

Each layer of the Transformer contains not just attention mechanisms but also feed-forward neural networks. These networks operate independently on each position, transforming the data after the attention mechanism has processed it.

Stacked Layers:

Both the encoder (which processes the input) and the decoder (which produces the output) in the Transformer are made up of multiple identical layers stacked on top of each other. This deep architecture allows the model to learn complex patterns and relationships.

Benefits:

The Transformer's parallel processing capability makes it faster than RNN-based models, especially on hardware accelerators like GPUs.
Its attention mechanisms allow it to handle long-range dependencies in data, making it particularly suited for tasks like machine translation.

Impact:

The Transformer architecture has revolutionized the field of natural language processing. Its design principles have been the foundation for models like BERT, GPT, and many others, which have achieved state-of-the-art results on a wide range of tasks.
Its influence extends beyond NLP, with researchers exploring its potential in other domains like computer vision.`,
    questions: [
      {
        question: 'Why is the paper cool?',
        correct_answer: "Things are cool.",
        other_answers: [
            "Objects are rad.",
            "I am a turtle",
        ],
      },
      {
        question: 'What is the paper about?',
        correct_answer: "things",
        other_answers: [
            "Stuff",
            "Junk",
            "Something",
        ],
      }
    ]
    }
  };

  getTitle(): string {
    return this.paperCurriculum.overview_module.name;
  }

  getContent(): string {
    return this.paperCurriculum.overview_module.blurb;
  }

  getQuestions(start: number, count: number): Observable<Question[]> {
    const currQuestions = this.paperCurriculum.overview_module.questions.slice(start, start + count);
    for (const question of currQuestions) {
      question.shuffled_answers = getAllAnswers(question);
    }
    return of(currQuestions);
  }

  getTotalContentCount(): number {
    return this.paperCurriculum.overview_module.questions.length;
  }
}
