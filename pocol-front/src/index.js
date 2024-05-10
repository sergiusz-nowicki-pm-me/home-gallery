import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ImageSetPanel } from "./pages/gallery/ImageSetPanel";
import { ImagePanel } from "./pages/gallery/ImagePanel";

const router = createBrowserRouter([
    {
        path: "/",
        // element: <App />,
        element: <div>test</div>,
        errorElement: <div>error</div>,
    },
    {
        path: "/gallery/:id",
        element: <ImageSetPanel />,
    },
    {
        path: "/gallery/:id/:file_no",
        element: <ImagePanel />,
    },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>
);
