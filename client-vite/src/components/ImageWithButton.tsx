import { FC, useContext } from 'react';
import { Image as AntdImage, Button } from 'antd';
import { PlusOutlined, MinusOutlined } from '@ant-design/icons';
import { ImageContext } from '../App';

type ImageProps = {
    src: string;
}

const ImageWithButton: FC<ImageProps> = ({ src }) => {
    const { searchFrame, positiveFrames, negativeFrames, modifyFeedback } = useContext(ImageContext);
    let borderStyle = '';
    if (positiveFrames.includes(src)) {
        borderStyle = '5px solid green';
    }
    if (negativeFrames.includes(src)) {
        borderStyle = '5px solid red';
    }
    return (
        <div className='image-container' style={{position: 'relative', border: `${borderStyle}` }}>
            <AntdImage
                src={src}
                preview={false}
                loading='lazy'
                onClick={() => searchFrame(src)}
            />
            <Button
                icon={< PlusOutlined />}
                className='top-right-button'
                onClick={() => modifyFeedback(1, src, false)}
            />
            <Button
                icon={< MinusOutlined />}
                className='top-left-button'
                onClick={() => modifyFeedback(1, src, true)}
            />
        </div>
    )
}

export default ImageWithButton;