import torch
from Model import Model,ModelArgs

if __name__=="__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # device = torch.device("cpu")
    
    if torch.cuda.is_available():
        print("use cuda")
        print(torch.__version__)
        print(torch.version.cuda)
    else:
        print("use cpu")

    args = ModelArgs(device = device, vocab_size=6400, embedding_dim=512)
    tokenizer, model = Model.init_model(args)


    new_prompt="什么山最高"
    answer = new_prompt
    with torch.no_grad():
        x = torch.tensor(tokenizer(new_prompt)['input_ids'], device=args.device).unsqueeze(0)
        outputs = model.generate(
            x,
            eos_token_id=tokenizer.eos_token_id,
            max_new_tokens=args.max_seq_len,
            temperature=0.4,
            top_p=0.9,
            stream=True,
            pad_token_id=tokenizer.pad_token_id
        )

        print('🤖️: ', end='')
        try:
            history_idx = 0
            for y in outputs:
                answer = tokenizer.decode(y[0].tolist(), skip_special_tokens=True)
                if (answer and answer[-1] == '�') or not answer:
                    print(answer)
                    continue
                print(answer[history_idx:], end='', flush=True)
                history_idx = len(answer)
        except StopIteration:
            print("No answer")
        print('\n')
