import {IoMdArrowRoundForward, IoMdArrowRoundBack} from 'react-icons/io';

const BackPageButton = (props) => {
    return (
        <button class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-8 rounded inline-flex items-center mx-6"
            onClick = {() => {

                let temp_cursors = props.cursors;

                temp_cursors.next_cursor = props.cursors.current_cursor;
                if(props.cursors.previous_cursor.length !== 1) temp_cursors.current_cursor = temp_cursors.previous_cursor.pop();
                props.setCursors(temp_cursors);
                props.searchRequest();
            }}
        >
            <IoMdArrowRoundBack className='w-6 h-6' />
        </button>
    );
}

export default BackPageButton;