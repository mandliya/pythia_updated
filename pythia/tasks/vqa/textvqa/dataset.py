# Copyright (c) Facebook, Inc. and its affiliates.
from pythia.tasks.vqa.vizwiz import VizWizDataset
from pythia.utils.text_utils import word_tokenize
import traceback


class TextVQADataset(VizWizDataset):
    def __init__(self, dataset_type, imdb_file_index, config, *args, **kwargs):
        super().__init__(dataset_type, imdb_file_index, config, *args, **kwargs)
        self._name = "textvqa"
        traceback.print_stack()

    def format_for_evalai(self, report):
        answers = report.scores.argmax(dim=1)

        predictions = []
        answer_space_size = self.answer_processor.get_true_vocab_size()

        for idx, question_id in enumerate(report.question_id):
            answer_id = answers[idx].item()
            if answer_id >= answer_space_size:
                answer_id -= answer_space_size
                answer = word_tokenize(report.context_tokens[idx][answer_id])
            else:
                answer = self.answer_processor.idx2word(answer_id)

            predictions.append({"question_id": question_id.item(), "answer": answer})
        return predictions
