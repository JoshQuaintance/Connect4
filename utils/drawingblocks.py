from types import SimpleNamespace


class DrawingBlocks:
    '''
    ASCII Drawing Blocks Characters

    Blocks
    ------
    ```
    \u2503 ~ VERTICAL_LINE

    \u2501 ~ HORIZONTAL_LINE

    \u250F ~ TOP_LEFT_CORNER

    \u2513 ~ TOP_RIGHT_CORNER

    \u2517 ~ BOTTOM_LEFT_CORNER

    \u251B ~ BOTTOM_RIGHT_CORNER

    \u252B ~ MIDDLE_CONNECT_LEFT

    \u2523 ~ MIDDLE_CONNECT_RIGHT

    \u253B ~ MIDDLE_CONNECT_UP

    \u2533 ~ MIDDLE_CONNECT_DOWN

    \u254B ~ FOUR_WAY
    ```

    Methods
    -------
    `getAll(return_format: str, block_type: str) -> SimpleNamespace or dict`
        Get all drawing blocks depending on the arguments
    '''

    __blocks_dict = {}
    blocks_namespace = None
    __double_dict = {}
    double_namespace = None

    def __init__(self):
        '''
        Single Blocks
        -------------
        ```
        \u2503 ~ VERTICAL_LINE

        \u2501 ~ HORIZONTAL_LINE

        \u250F ~ TOP_LEFT_CORNER

        \u2513 ~ TOP_RIGHT_CORNER

        \u2517 ~ BOTTOM_LEFT_CORNER

        \u251B ~ BOTTOM_RIGHT_CORNER

        \u252B ~ MIDDLE_CONNECT_LEFT

        \u2523 ~ MIDDLE_CONNECT_RIGHT

        \u253B ~ MIDDLE_CONNECT_UP

        \u2533 ~ MIDDLE_CONNECT_DOWN

        \u254B ~ FOUR_WAY
        ```

        Double Blocks
        -------------
        ```
        \u2551 ~ D_VERTICAL_LINE

        \u2550 ~ D_HORIZONTAL_LINE

        \u2554 ~ D_TOP_LEFT_CORNER

        \u2557 ~ D_TOP_RIGHT_CORNER

        \u255A ~ D_BOTTOM_LEFT_CORNER

        \u255D ~ D_BOTTOM_RIGHT_CORNER

        \u2563 ~ D_MIDDLE_CONNECT_LEFT

        \u2560 ~ D_MIDDLE_CONNECT_RIGHT

        \u2569 ~ D_MIDDLE_CONNECT_UP

        \u2566 ~ D_MIDDLE_CONNECT_DOWN

        \u256C ~ D_FOUR_WAY
        ```
        '''

        self.__blocks_dict = {
            'VERTICAL_LINE': '\u2503',
            'HORIZONTAL_LINE': '\u2501',
            'TOP_LEFT_CORNER': '┏', #\u250F
            'TOP_RIGHT_CORNER': '\u2513',
            'BOTTOM_LEFT_CORNER': '\u2517',
            'BOTTOM_RIGHT_CORNER': '\u251B',
            'MIDDLE_CONNECT_LEFT': '\u252B',
            'MIDDLE_CONNECT_RIGHT': '\u2523',
            'MIDDLE_CONNECT_UP': '\u253B',
            'MIDDLE_CONNECT_DOWN': '\u2533',
            'FOUR_WAY': '\u254B'
        }

        self.blocks_namespace = SimpleNamespace(**self.__blocks_dict)

        self.__double_dict = {
            'D_VERTICAL_LINE': '\u2551',
            'D_HORIZONTAL_LINE': '\u2550',
            'D_TOP_LEFT_CORNER': '\u2554',
            'D_TOP_RIGHT_CORNER': '\u2557',
            'D_BOTTOM_LEFT_CORNER': '\u255A',
            'D_BOTTOM_RIGHT_CORNER': '\u255D',
            'D_MIDDLE_CONNECT_LEFT': '\u2563',
            'D_MIDDLE_CONNECT_RIGHT': '\u2560',
            'D_MIDDLE_CONNECT_UP': '\u2569',
            'D_MIDDLE_CONNECT_DOWN': '\u2566',
            'D_FOUR_WAY': '\u256C'
        }

        self.double_namespace = SimpleNamespace(**self.__double_dict)

    def getAll(self, return_format: str = 'dict', block_type: str = 'all') -> SimpleNamespace or dict:
        ''' 
        Gets all the blocks according to the arguments

        It can be specified if it should return a dict or namespace by passing
        the argument `return_format`.

        It can be specified if it should return a single line block or double 
        by passing the argument `block_type`

        Parameters
        ----------
        `return_format : str, optional`
            The data structure to get ('dict' or 'namespace')

        `block_type : str, optional`
            The block type to get ('single', 'double')
        '''

        both_dicts = {**self.__blocks_dict, **self.__double_dict}
        both_namespace = SimpleNamespace(**both_dicts)

        if (return_format == 'dict'):

            if (block_type == 'all'):
                return both_dicts

            if (block_type == 'single'):
                return self.__blocks_dict

            if (block_type == 'double'):
                return self.__double_dict

        if (return_format == 'namespace'):
            if (block_type == 'all'):
                return both_namespace

            if (block_type == 'single'):
                return self.__blocks_namespace

            if (block_type == 'double'):
                return self.__double_namespace


'''

┳  ━╋━━━━━━━━━━
┻━━━━━
'''

# Single Blocks
VERTICAL_LINE= '\u2503'
HORIZONTAL_LINE= '\u2501'
TOP_LEFT_CORNER= '\u250F'
TOP_RIGHT_CORNER= '\u2513'
BOTTOM_LEFT_CORNER= '\u2517'
BOTTOM_RIGHT_CORNER= '\u251B'
MIDDLE_CONNECT_LEFT= '\u252B'
MIDDLE_CONNECT_RIGHT= '\u2523'
MIDDLE_CONNECT_UP= '\u253B'
MIDDLE_CONNECT_DOWN= '\u2533'
FOUR_WAY= '\u254B'

# Double Blocks
D_VERTICAL_LINE= '\u2551',
D_HORIZONTAL_LINE= '\u2550',
D_TOP_LEFT_CORNER= '\u2554',
D_TOP_RIGHT_CORNER= '\u2557',
D_BOTTOM_LEFT_CORNER= '\u255A',
D_BOTTOM_RIGHT_CORNER= '\u255D',
D_MIDDLE_CONNECT_LEFT= '\u2563',
D_MIDDLE_CONNECT_RIGHT= '\u2560',
D_MIDDLE_CONNECT_UP= '\u2569',
D_MIDDLE_CONNECT_DOWN= '\u2566',
D_FOUR_WAY= '\u256C'