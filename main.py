try:
    import pygame
except ModuleNotFoundError:
    print("Please install pygame")
else:
    from graphics import main

    main()
