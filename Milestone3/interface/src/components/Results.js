const Results = (props) => {
    console.log(props.books);
    return (
        <div className="w-[65%]">
            <div className="bg-gray-200 p-8 rounded-md">
            {props.books.length === 0 ? <div className="text-2xl">No results found</div> : null}
                {props.books.map((book) => (
                    <div className="flex flex-row mb-8 text-left"
                        onClick = {() => {
                            // open new tab 
                            window.open("http://www.amazon.com/exec/obidos/ASIN/" + book.id);
                        }}

                    >
                        <div className="w-1/3">
                            <img src={book.imgUrl
                                ? book.imgUrl
                                : "https://via.placeholder.com/150"} alt="book cover"/>
                        </div>
                        <div className="w-2/3">
                            <h1 className="text-2xl font-bold" 
                                dangerouslySetInnerHTML={{__html: book.title}} 
                                ></h1>
                            <h2 className="text-lg font-bold">{book.brand}</h2>
                            <p className="text-sm">{book.description}</p>
                            <p className="text-sm">{book.price ? book.price : "NaN"}</p>
                            {
                                [...Array(Math.floor(book.overall))].map(
                                    (e, i) => <i key={i} className="fas fa-star"></i>
                                )
                            }
                            <p className="text-sm">{book.category}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Results;