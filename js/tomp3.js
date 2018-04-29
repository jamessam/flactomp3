const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const hiResPath = process.argv[2];
const loResPath = process.argv[3];
const extension = process.argv[4];

const validExtensions = ['flac', 'wav'];

function InvalidExtension(error) {
  this.error = error;
  this.name = 'InvalidExtension';
}

function PathNotFoundError(error) {
  this.error = error;
  this.name = 'PathNotFoundError';
}

function checkPath(path, value) {
  if (!fs.existsSync(path)) {
    throw new PathNotFoundError(
      `That value for the ${value} is invalid. Please try running the script again.`
    );
  }
  return;
}

function convertFile(f) {
  // TODO: Find out how many channels are in the file

  let low = f.replace(extension, 'mp3');
  // This command will change once varying channels are supported.
  let ffmpegCommandArgs = [
    '-i',
    `${path.join(hiResPath, f)}`,
    '-write_id3v1',
    '1',
    '-id3v2_version',
    '3',
    '-dither_method',
    'modified_e_weighted',
    '-out_sample_rate',
    '48k',
    '-b:a',
    '320k',
    `${path.join(loResPath, low)}`
  ];

  const promise = new Promise((resolve, reject) => {
    const ffmpeg = spawn('ffmpeg', ffmpegCommandArgs);
    ffmpeg.stderr.on('data', data => {
      console.log(`Processing for ${f} failed:`)
      console.log(`${data}`);
    });
    ffmpeg.on('close', code => {
      resolve();
    });
  });

  return promise;
}

function makeFileList(path, extension) {
  let files = new Array();
  const rawList = fs.readdirSync(path);
  rawList.map(f => {
    const tempExtIndex = extension.length;
    let tempFExt = f.substring(f.length - tempExtIndex, f.length);
    // TODO: This needs to be extended to allow for capitalization variance
    if (tempFExt === extension) {
      files.push(f);
    }
  });
  return files;
}

function validateExtension(extension) {
  if (validExtensions.indexOf(extension) === -1) {
    throw new InvalidExtension(`${extension} is not a valid format.`);
  }
  return;
}

// Synchronously validate if FFMPEG is added to the system

// Synchronously validate the paths passed from the cli and the format is valid
try {
  checkPath(hiResPath, 'high resolution path');
  checkPath(loResPath, 'low resolution path');
  validateExtension(extension);
} catch (error) {
  console.log(error.error);
  process.exit();
}

// Synchronously make the file list
const fileList = makeFileList(hiResPath, extension);

// Map through the file list and create mp3s
fileList.map(f => {
  // TODO: check if mp3 already exists
  convertFile(f);
});
