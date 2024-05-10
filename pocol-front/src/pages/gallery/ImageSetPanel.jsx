import axios from "axios";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

export function ImageSetPanel() {
    let { id } = useParams();
    const [data, setData] = useState({ id: "", images: [] });

    useEffect(() => {
        const imageSetLoader = async (id) => {
            let responce = await axios.get(
                "http://localhost:8081/query/get-image-set/" + id
            );
            setData(responce.data.data);
            console.log(responce.data.data);
        };
        imageSetLoader(id);
    }, [id]);

    return (
        <div>
            Test: {data.id}
            {Object.keys(data.images).map((i) => {
                return (
                    <Link to={"/gallery/" + id + "/" + i}>
                        {data.images[i]}
                    </Link>
                );
            })}
        </div>
    );
}
