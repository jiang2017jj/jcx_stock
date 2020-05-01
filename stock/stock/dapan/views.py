from stock.dapan import dapan_blue

@dapan_blue.route('/',strict_slashes=False)
def helloword():
    return 'hello ! jj'