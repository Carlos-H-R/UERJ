def check(min_votes: int, votes: list) -> bool:
    


n = int(input())

for i in range(n):
    n_votes = int(input())
    votes = list(map(str, input().split()))

    has_sec_turn = check(n_votes//2, votes)

    if has_sec_turn:
        print('S')

    else:
        print('N')
