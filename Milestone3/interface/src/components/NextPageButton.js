import {IoMdArrowRoundForward, IoMdArrowRoundBack} from 'react-icons/io'; 

const NextPageButton = (props) => {
    return (
        <button className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-8 rounded inline-flex items-center mx-6"
            onClick = {(event) => {
                let temp_cursors = props.cursors;



                temp_cursors.previous_cursor.push(props.cursors.current_cursor);
                temp_cursors.current_cursor = props.cursors.next_cursor;
                
                props.setCursors(temp_cursors);
                
                
                props.searchRequest(event);
            }}
        >
            <IoMdArrowRoundForward className='w-6 h-6' />
        </button>
    );
}

export default NextPageButton;