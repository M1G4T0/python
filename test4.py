def russian_roulette (c):
    import random
    chamber = [1,2,3,4,5,6]
    bullet = random.choice(chamber)
    while len(chamber) != 1:
        if c == bullet:
            print('You died')
            return 'Loser'
        else:
            chamber.remove(c)
            c = int(input('Joga outra vez\n>>'))
    return 'Winner'
x = int(input())
russian_roulette(x)