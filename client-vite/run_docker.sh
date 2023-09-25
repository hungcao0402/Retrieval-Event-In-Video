docker run -it -d \
    -v /mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/client-vite:/client \
    -v /mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/Keyframe_Compress:/client/public/Keyframe \
    --network host \
    --name client_dev \
    node:18.17.1-bullseye 