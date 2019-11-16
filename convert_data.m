function data=convert_data(source_root_dir, target_root_dir, imname, cname, fine_height, fine_width)
    % generate image
    im = imread([source_root_dir 'image/' imname]);
    im = imresize(im, [fine_height, fine_width], 'bilinear');
    imwrite(im, [target_root_dir 'image/' imname]);

    % generate cloth mask
    im_c = imread([source_root_dir 'cloth/' cname]);
    im_c = imresize(im_c, [fine_height, fine_width], 'bilinear');
    imwrite(im_c, [target_root_dir 'cloth/' cname]);

    % save cloth mask
    mask = double((im_c(:,:,1) <= 250) & (im_c(:,:,2) <= 250) & (im_c(:,:,3) <= 250));
    mask = imfill(mask);
    mask = medfilt2(mask);
    imwrite(mask, [target_root_dir 'cloth-mask/' cname]);

    data = 0
end

