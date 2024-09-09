const Filters = (props) => {
    // filter are facets
    return (
          <div className="flex flex-col w-[35%]  text-center ">
            <div className="bg-gray-200 mr-12 py-6 px-10 rounded-md">
                <h1 className="text-2xl font-bold mb-4">Filters</h1>
                <div className="flex flex-col">
                    {props.facets.map((facet, index) => (
                        <div className="flex flex-row">
                            <p className="text-sm">{facet.facet}</p>
                            <p className="text-sm"> ({facet.num})</p>
                            <input type="checkbox" id={facet.facet} name={facet.facet}
                            
                            onClick = {(event) => {
                                let temp_facets = props.facets
                                temp_facets[index].checked = !facet.checked;
                                props.setFacets(temp_facets);
                            }}
                            
                            />
                        </div>
                    ))}
                </div>
             </div>
         </div>
     );
 }

 export default Filters;