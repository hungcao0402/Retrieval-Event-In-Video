import { useState, FC } from 'react';
import { List, Slider } from 'antd';
import { ImageWithButton } from '.';

const colCounts: Record<number, number> = {};

[4, 5, 6, 7, 8, 9, 10].forEach((value, i) => {
    colCounts[i] = value;
});


type ImageGridProps = {
    paths: string[];
};

const ImageGrid: FC<ImageGridProps> = ({ paths }) => {
    const [colCountKey, setColCountKey] = useState<number>(3); // Slider
    const colNum: number = colCounts[colCountKey]; // Slider

    return (
        <div className='flex-col'>
            <div className='flex-row'>
                <span>Column Count</span>
                <Slider
                    min={0}
                    max={Object.keys(colCounts).length - 1}
                    value={colCountKey}
                    onChange={setColCountKey}
                    marks={colCounts}
                    step={null}
                    style={{ width: '30%' }}
                />
            </div>
            <List
                grid={{ gutter: 8, column: colNum }}
                dataSource={paths}
                renderItem={(path) => (
                    <div>
                        <List.Item>
                            <ImageWithButton src={path} />
                        </List.Item>
                    </div>
                )}
            />
        </div>
    )
}

export default ImageGrid
