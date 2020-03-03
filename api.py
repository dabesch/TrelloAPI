import getFiles
from auth import getKeys

key, token = getKeys()
board = '5e5d12afee1a6134b7cd48c8'

getFiles.run(board, key, token)
